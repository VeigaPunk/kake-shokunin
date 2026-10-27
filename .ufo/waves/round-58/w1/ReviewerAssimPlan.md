# ReviewerAssimPlan

Scope reviewed: round prompt §10 (kake-round-58.md lines 491–597), frozen contract `contract.md` + `contract.json`, `assimilation/` contents (collisions, staged-ids, reg-ids, quarantine-slice, mirror-pin.json, pre-append mirror), `merge/kake/MERGE-REPORT.md` + `SOURCES.append.md` + `knowledge/`, retained bodies `sources/S423.html`/`S424.html` + `receipts.json`, `validate_append.sh`, `span_tools.py`. All checks run read-only from scratch (`/fast/scratch/hyaku/kake-r58/ReviewerAssimPlan`); no lane mutation.

## CHECKLIST:

**1. Id lists and collision count (recomputed) — PASS.** Ran the §10 command verbatim against `corpus/SOURCES.md` and `merge/kake/SOURCES.append.md`: reg-ids = 160 rows (S001–S140, S249, S262–S263, S273–S274, S286, S312, S329, S367, S372–S374, S390, S409, S416–S422); staged-ids = 129 rows (S287–S415); collisions = 8: **S312 S329 S367 S372 S373 S374 S390 S409** — identical to the committed `assimilation/{reg-ids,staged-ids,collisions}` and to the contract's collision line. Neither S395 nor S378 collides.

**2. Guard proof — PASS.** Fixture: scratch registry with indented row `  | S002 |` colliding with staged set → `collisions` nonempty (S002). The 0–3-space pattern catches indented collisions as required. Committed `collisions` is therefore trustworthy.

**3. Renumber by document (S395 → S423) — PASS.** Staged S395 (URL id=3457) is re-id'd to S423 by the URL/anchor, not arithmetic (id follows evidence). S423 is the next free id after registry max S422. `mirror-pin.json` records adoptedAbsent S423/S424 (pre-append mirror has 160 rows, sha256 `57c83362…`, byte-identical to the lane's current `corpus/SOURCES.md` — no registry drift since pin at base 0440485).

**4. S424 lane-found (not from package) — allowed, PASS.** URL `…articleinfo?id=3028` appears **0 times** in `SOURCES.append.md` (not staged); it is linked **from inside S423.html** (`articleinfo?id=3028` found in the retained body); retained with receipt (sha256 `3ef1275b…` matches `receipts.json`). Contract C3 defines S424 as lane-found — permissible: the admission subject is knowledge entries, and a row the lane opens itself (linked from an admitted source) is valid ground, id free in registry.

**5. Only rows admitted entries cite — PASS (planned).** Append block = exactly S423 + S424; used-by cells name exactly the two admitted entries. No bulk-append of the 129-row package.

**6. Recheck cell normalised — REQUIRED, demonstrated.** Staged rows are campaign-schema: recheck = `180d — curl … \| grep … -> 1 (ran 2026-10-24)` with escaped `\|` pipes (quoted in `SOURCES.append.md` rows S395/S378). Normalized form (scratch): recheck = `180d`; the stripped verification-command prose must be recorded in the round lesson's Gate block. Opened must be the lane's own access date 2026-10-26 (not campaign 2026-10-24).

**7. No pipe in cells — PASS (normalized rows).** S423/S424 rows each contain exactly 12 `|` (11 columns); zero `\|` escapes anywhere in the mirror.

**8. Scratch census validation before append — PASS (replicated, exit 0).** Rebuilt the `validate_append.sh` mirror in scratch (whole `corpus/` + non-corpus used-by targets SCORECARD.md, SKILL.md, scripts/source_recheck.py, round-41 c1_count.py/oracle_crosscheck.py), inserted the normalized S423/S424 rows at the end of the Registry table, added the two entry files at repo-relative paths, and ran `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → **exit 0**; only pre-existing W04 duplicate-url warnings (S033/S088/S092/S098/S099/S102/S110/S111/S115/S116/S117/S127/S416/S417), no E03/E04 on the new rows. (The lane's `assimilation/validate/` does not exist yet — run the script before the real append.)

**9. Quarantine slice handled — PASS.** Re-derived slice from `absent-defect-register.md` (kake rows): 12 rows — 9 payload-absent (S142 S143 S148 S156 S161 S193 S194 S195 S206), 3 prose/unfetchable class (S154 S178 S184). Identical to committed `quarantine-slice`. None intersects adopted ids; nothing from the slice is adopted; the prose class is marked unverifiable (`unreachable`), not fabrication.

**10. ≥1 admit and ≥1 reject — PASS (planned).** Admit: `baidu-spider-identification.md` (cites S423), `baidu-spider-unblocking.md` (cites S424). Reject: staged `yahoo-japan-crawler-address-change-notice.md` (S378) — LINE Yahoo ads API Display Ads product-list crawler (FTP periodic fetch), not a search crawler; gated against PROVINCE; reason + flip condition must sit in the Gate block and stay refused until cleared.

**11. Gate quotes — PASS (verified spans).** `span_tools.py` (uses C3 counter's own article-block/text-node code): S423 `"非*.baidu.com或*.baidu.jp即为冒充。"` → 6 units/28 chars, in a text node, unique across both bodies; S424 `"常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。"` → 20 units/33 chars, unique (also `"解除百度UA封禁：查看网站反爬虫策略，进行策略调整。"` 21u/26c unique). Both within ≤25 units/≤40 chars; Gate must use ASCII double quotes.

**12. doctrine/ unused — PASS.** `merge/kake/doctrine/` does not exist; no doctrine material is used; only chousa may judge it as a source.

**13. MERGE-REPORT.md consulted — PASS.** The report names both staged entries in its knowledge table: `baidu-crawler-identification.md` (round14: "The operator publishes its crawler names *and* tells you not to trust them") and `yahoo-japan-crawler-address-change-notice.md` (round11). S395/S378 ids are not printed in the report (ids exist only in `SOURCES.append.md`); the mapping is via the entry filenames. Report also confirms staged rows 129 / entries 104, adopt checklist, and used-by pointer corrections.

**14. One theme, 1–3 entries — PASS.** Theme: Baidu crawler identification; 2 entries.

## GAPS:

- The two adopted knowledge files do not exist in the lane yet (pre-append). Executor must draft `corpus/knowledge/baidu-spider-identification.md` and `corpus/knowledge/baidu-spider-unblocking.md`, each citing exactly its own row and carrying access date 2026-10-26. Existing lane file `baidu-spider3-dead-link-model.md` does not collide with these names.
- The lesson `## Gate` block must record: lane access dates, the located quotes above, the admit list (2), the reject (S378) with reason + flip, and the stripped recheck prose (campaign verification commands).
- `assimilation/validate/` is not yet populated — `validate_append.sh` must run (exit 0) before the first registry append; round end still requires `sources-census.sh validate --root <lane> kake` exit 0.
- Report must paste both id lists, the 8 collision ids and the renumber map S395 → S423 (this review supplies them above).

## ORDER OF OPERATIONS:

1. In scratch: (a) re-run guard fixture (proven above, S002 caught); (b) paste staged S395 row; (c) normalize to S423 row (11 cols, no pipes, recheck `180d`); (d) draft S424 row from S423-linked body (opened 2026-10-26).
2. Draft the two entries with Gate quotes from §11.
3. Run `validate_append.sh` (or the exact mirror recipe): exit 0 required before append.
4. Apply to lane: insert S423/S424 rows at the end of the Registry table (after S422), write the two entries, update the lesson Gate (admits + S378 reject), keep report evidence.
5. Run C3 counter (`c58_quote_truth.py`) expecting 8/8; run C2 counter (12/12) and C1 counter (met) per contract.
6. Round end: `sources-census.sh validate --root <lane> kake` exit 0.

VERDICT: Assimilation plan is sound and all gate preconditions verified feasible (collisions 8, renumber S395→S423, S424 lane-found allowed, census exit 0, quotes valid, quarantine and rejects handled); execute in the stated order, completing the entry drafts and Gate block before append.
