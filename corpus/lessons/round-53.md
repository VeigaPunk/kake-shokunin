# Round 53 — kake

Lane: `kake-shokunin`; base `3994101dba28896830604fd0b08c7f00faca8ed6`.

## Gate

No new source rows were written. The round-52 admits and refusals were re-opened against retained bodies and package evidence; their source decisions stand, but the gate rationale requires correction. The source census at round start was 148 rows and exit 0 (12 W04 duplicate-URL warnings).

### Round-52 corrections (append-only)

The round-52 verifier spot-check is a protected non-author artifact and is not edited. Its claim that S367, S372, S373, S390 and S409 resolve only in kotodama is misleading: these ids denote unrelated history sources in kotodama, but in the shokuknow kake staging package they were the intended Yahoo/Baidu rows, never admitted to kake. The three round-52 entries cited staged ids as held ground. `SOURCES.md` census validates registry rows, not prose citations. Read-only seat evidence: `.ufo/waves/round-53/w1/ReviewerProvenance.md`, `.ufo/waves/round-53/w1/CriticCrossLane.md`.

S329's quoted PC/mobile clause is under `如何正确识别Baiduspider移动ua`; its wildcard quote is under `robots写法`, and its spider-trap quote under `使用robots巧妙避免蜘蛛黑洞`. The page prints the course-header marker `最新更新章节：2019-09-18`; it is not a section date. S312's quoted list is under `如何提升移动适配效果`, introduced by `以下是常见的对应不准确错误`; `常见原因` is absent, and `2020-08-14` is a page-header marker, not a section timestamp. Read-only evidence: retained bodies `.ufo/waves/round-52/sources/S329.html` and `S312.html`; seats `.ufo/waves/round-53/w1/ScoutS329.md`, `ScoutS312.md`, `CriticLocators.md`.

The two refusals remain refusals. CrUX keyless sources S303/S304 were unopened and unregistered in round 52 (CORPUS rule 1); the held field-performance entry does not contain the keyless rule. The Jekyll staged source was unopened in round 52; the claim that the refusal follows from E04 duplicate-in-scope is not established (census E04 requires matching scope; see `ScribeGate.md`). Do not treat the verifier's approved duplicate-ground narrative as established.

## Mistakes

|Class|Evidence|Captured-by|Fix|
|---|---|---|---|
|Staged, unadmitted source ids presented as lane-held ground|Round-52 entries cite S367/S372/S373/S390/S409, absent from kake registry; ids coincide with unrelated kotodama records but point to intended pages only in the unadmitted shokuknow package. Census exit 0 does not inspect prose ids.|No criterion checked whether knowledge-entry citations resolve to the lane's own registry; the sources census checks registry shape/used-by path existence only.|Append a QUALITY criterion requiring source ids in knowledge prose to resolve in kake's own registry at the citing revision, and retract unsupported staged claims. The initial failing state is committed round-52 tip `3994101`; verification must measure the correction, not a green census.|
|Quote locator copied from package description rather than source section|S329/S312 Gate and knowledge locators disagree with retained bodies; nearest headings and date-scope described above.|Round-52 quote counter C5 checks quote substring and size, not heading/section location; no locator criterion.|Add append-only correction blocks and superseding registry rows; preserve round-52 bytes. S329 correction must retain all three distinct quote headings.|
|Refusal decision supported by an incorrect reason|Round-52 refusal section says CrUX ground already held and Jekyll E04 duplicate-in-scope; neither reason follows from the evidence.|No explicit review of staged source open/receipt population and E04's same-scope condition.|Keep decisions but append corrected reasons: unopened/unregistered this round for CrUX; Jekyll entry likewise unopened in-round. Do not claim E04 without same-scope evidence.|
|Round-52 work omitted from LOG|Verifier spot-check §1 reports no round-52 LOG entry; current LOG's last lines are round-51.|Round rule required LOG activity, but no round entry written.|Append round-52 correction and round-53 activity with landed hashes; never rewrite prior LOG bytes.|
|Source qualifier inverted in translation|The S374 source phrase `巡回を推奨していない` includes a crawl qualifier; the round-52 English gloss reduced it to an endorsement-only statement. Independent round-53 seat review also found the source title/meta frames it as link-target crawl restriction. This claim was not re-opened by the L1 in this round.|No criterion catches whether translations preserve a material source qualifier; this remains open for a fresh L1 source re-open.|Do not treat S374's entry as semantically re-verified. Re-open the source and append a correction in a later round before claiming quality improvement.|

## Assimilation and frontier

Assimilation: none. The kake package is stale against the lane's 148-row registry and includes the twelve quarantine-slice rows; no package rows were adopted. The quarantine slice has 12 ids (S142, S143, S148, S156, S161, S193, S194, S195, S206, S154, S178, S184), with nine payload-absent and three unreachable classes; no rows were hand-checked this round (seat `.ufo/waves/round-53/w1/ScoutQuarantine.md`).

Considerthese: `considerthese/2026-10-24.md` was opened read-only. Its proposal to compare unmerged branches by tree diff is not implemented this round; recorded here as an unimplemented proposal, not evidence or a source row.

No tools were installed or updated.

## Gate

Five missing kake rows identified in the round-52 verifier review were opened by the executor this round and appended to `corpus/SOURCES.md` as S367, S372, S373, S390 and S409. URLs, exact quotes, located anchors, access date, HTTP status, byte counts and SHA-256 digests are recorded in `.ufo/waves/round-53/sources/gate-draft.md`; retained bodies and fetch receipts are in `.ufo/waves/round-53/sources/`. The staged ids also occur in kotodama's registry but mean unrelated material there; the intended pages are in shokuknow's kake package. The package rows were not copied blindly: the individual-link refusal claim was withdrawn for S367, S390's date and heading were corrected, and S372's anchor was widened to cover its claims. S390/S409 do not say that the crawler executes script.

- S416 — https://ziyuan.baidu.com/college/courseinfo?id=1399 — accessed 2026-10-25 — § 友好抓取 → 如何正确识别Baiduspider移动ua (course-header 最新更新章节 2019-09-18; no section date) — quote: "如果封禁的agent是Baiduspider，会对PC和移动同时生效" (retained body `.ufo/waves/round-53/sources/S329-reread.html`, 61418 bytes, sha256 `fa69c284d785cb925b3945a9a8327f9ba20ed2103b02743930ff9d5deee3f949`; quote occurs once).
- S417 — https://ziyuan.baidu.com/college/courseinfo?id=267&page=15 — accessed 2026-10-25 — § 移动适配 → 如何提升移动适配效果, list introduced by 以下是常见的对应不准确错误 (course-header 最新更新章节 2020-08-14; no section date) — quote: "手机页使用了ajax等异步加载的方法加载内容主体" (retained body `.ufo/waves/round-53/sources/S312-reread.html`, 46056 bytes, sha256 `2b4d8116f42b7d661568a59595413ac504afd815107549fc48eb2b40b9e415c5`; quote occurs once).

These two superseding rows correct anchor/date metadata only; they do not amend the previously admitted source claims or claim that the S312 list is a formal rejection-cause list.

## Round-52 routed-defect disposition

1. Push/ancestry: round-52 closure pushed the six round-52 commits; this round's branch was brought to a verified remote tip. Final lane report cites the exact landed commit.
2. Missing LOG: round-52 correction and round-53 entries are appended in `LOG.md`; hashes appear in subsequent appended lines.
3. Report sections: the round-53 fleet report uses the required section order and one measured revision.
4. Unregistered S367/S372/S373/S390/S409 references: corrected by opening and registering those sources; these are kake's staged ids, not cross-lane evidence. A broader automated citation checker is not added this round.
5. S329/S312 locators and date scope: append-only superseding rows S416/S417 plus correction blocks in both knowledge entries; round-52 lesson and entries remain historical.
6. Refusal reasons: decisions remain refusals. CrUX sources were unopened/unregistered; Jekyll source was unopened in-round. The duplicate-in-scope/E04 explanation is withdrawn as unsupported; no substitute claim of E04 is made.
7. Gate registry descriptions: not repaired; the existing counter checks row shape, not truth of registry cells. A robust registry-content gate would require a separately frozen claim and controls.
8. Receipt reproducibility: not repaired. The inherited mutation-ladder receipt was committed as it stood; its throwaway revision strings are nondeterministic. No reproducibility credit is claimed.
9. `final-verify.txt` fidelity: not regenerated; the round-52 receipt remains historical and its mismatch is not relabelled as verified.
10. Freshness-pin premises: not changed. The round-52 plazir/ds4cc pin rationale needs a fresh source-side recheck; no new pin verdict is claimed.
11. Dirty mutation-ladder receipt: committed with the round-53 evidence set, but this only resolves the uncommitted-file state; it does not repair the nondeterminism in item 8.
