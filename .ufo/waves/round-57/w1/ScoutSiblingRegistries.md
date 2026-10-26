# ScoutSiblingRegistries

SCRIPT:
- `.ufo/waves/round-57/w1/ScoutSiblingRegistries.files/survey.py` (table + ids; output `survey.out`) and `hazards.py` (fence/ordering/column/URL pass; output `hazards.out`). Both read-only, python3 stdlib, run once each. Census regex `^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|` ported to bytes regex; HEAD compare = `git -C <lane> show HEAD:corpus/SOURCES.md` vs working tree (byte compare, equivalent to cmp). No tools installed.
- Cross-check: `grep -cE` census count agrees with script for kake (158).

TABLE: (21 lanes, 21 files present, none missing; all values below were identical across lanes unless stated)
Constant for every lane: `## Registry` heading present exactly once (line-anchored); rows with 1-3 leading spaces = 0; rows with 4+ (or tab) leading spaces = 0; CRLF = 0; duplicate ids in file = 0; ids with 4+ digits = 0; rows outside `## Registry` = 0; non-census `|S..` lookalike rows = 0; rows inside code fences = 0; every census row has exactly 11 pipe-delimited fields (10 cells), so no embedded `|` shifts columns.
lane | census rows | id range | wt vs HEAD | non-monotone order
audio | 15 | S001-S015 | same | no
chousa | 106 | S001-S106 | same | no
game-dev-2d | 31 | S001-S031 | same | no
game-dev-3d | 36 | S001-S036 | same | no
kagi | 51 | S001-S051 | same | no
kaidoku | 106 | S001-S106 | same | no
kake | 158 | S001-S420 | same | yes (S262 after S286; S329 after S374; S312 after S329)
kama | 203 | S001-S329 | DIFF (+2 rows S328, S329 uncommitted) | no
kasegi | 48 | S001-S048 | DIFF (+S048 row and 2 prose lines in later section uncommitted) | no
kengaku | 100 | S001-S107 | same | yes (S081 after S091; S094 after S100)
kotoba | 142 | S001-S211 | same | yes (S211 after S216)
kotodama | 804 | S001-S880 | same | no
kumitate | 139 | S001-S200 | same | yes (S126 after S136); 4 lines trailing whitespace
lore | 32 | S001-S032 | same | no
mado | 226 | S001-S289 | same | yes (S218 after S277)
mori | 257 | S001-S484 | same | no
revenger | 49 | S001-S049 | same | no
souji | 139 | S001-S215 | same | no
tabi | 107 | S001-S107 | same | no
tameshi | 120 | S001-S260 | same | no
tsukuroi | 207 | S001-S207 | same | no
Gaps: ids are sparse in kake, kengaku, kotoba, kumitate, mado, mori, souji, tameshi (count < max id). Total census rows across lanes = 3,078.

IDS: (only kake and kotodama hold any of the five; every other lane's max id is below S367, except mori S484 / kotodama S880 / kake S420; mori holds none of them)
- S367: kake L157 https://info-search.yahoo.co.jp/archives/002852.php ; kotodama L396 https://periodicos.ufpb.br/index.php/srh/article/view/13999/7921 (unrelated paper)
- S372: kake L158 https://info-search.yahoo.co.jp/archives/002849.php ; kotodama L401 https://museu.socgeografialisboa.pt/objectos/padrao-de-santo-agostinho/
- S373: kake L159 https://info-search.yahoo.co.jp/archives/002850.php ; kotodama L402 https://eve.fcsh.unl.pt/en/places/rocks-ielala
- S390: kake L160 https://ziyuan.baidu.com/wiki/990 ; kotodama L419 https://repository.up.ac.za/bitstreams/902842e3-d5eb-4688-bf3f-40b310b24959/download
- S409: kake L161 https://ziyuan.baidu.com/wiki/1021 ; kotodama L438 https://web.archive.org/web/20151110063110/http://www.metmuseum.org/exhibitions/listings/2015/kongo/blog/posts/kongo-textiles-renaissance-european-collections
All ten rows sit under `## Registry`. URL location: column 2 (the source cell), form `<title> — <URL>`; kotodama appends a parenthetical access note after the URL. Ids S403 and S408 (the staged ids for S421/S422) have 0 census rows in kake's registry (kake's top id is S420, L166).
Consequence: ids are lane-local, not global. The same id means a different source in kake and kotodama (5/5 sampled collide).

PARSER HAZARDS: (a parser keyed to `## Registry` + 0-3 leading spaces)
1. Cross-lane id collision: any resolver that merges lanes by bare id returns two different sources for S367/S372/S373/S390/S409 (kake x kotodama); must key on (lane, id) or require a lane argument and report ambiguity.
2. Heading-like prose: kotoba has lines beginning `## Leads (unopened)` + backtick text inside paragraphs (placement-defect notes); a "next `##` heading ends the section" rule is still safe for Registry (registry precedes them) but a heading-list parser mis-reads them as sections. Other extra `##` sections (Registry changes in kasegi, Id allocation in tameshi, correction sections in kama, Search-log erratum in kagi) follow Registry; none contain census-matching rows today (0 rows outside Registry).
3. Non-monotone / sparse ids (kake, kengaku, kotoba, kumitate, mado, plus sparse in kake/mori/souji/tameshi): do not infer position or row count from max id; do not binary-search; "max id = count" is false in 8 lanes.
4. Dirty working trees: kama (+S328, S329) and kasegi (+S048) differ from HEAD; a resolver reading HEAD would miss them, one reading the working tree sees uncommitted rows. State which it uses.
5. Not mis-read today (verified 0): CRLF, leading-space 1-3 or 4+, tab-indented rows, duplicate ids within a file, 4-digit ids, rows inside fences, rows outside Registry, missing file. A `\d{3}` exact-three-digit id regex would still pass today (no S0001) but the census rule `S[0-9]{3,}` accepts 4 digits; resolver should too. A 4+-space/tab row would be silently dropped by a census-rule parser, which is correct under the lane census rule and absent today.
6. Free-text cells are long and contain `—`, backticks, parentheses, CJK, and `https://` URLs inside the title cell; extract URL by regex on the source cell, not by splitting on `—` (kotodama notes append a second parenthetical with HTTP/size text; kake cells contain `§` and `→`). Cell count is a constant 10 so `|` splitting is safe today.
7. Lines with trailing whitespace (kumitate x4) do not affect the row regex but would break exact-line equality checks.

VERDICT: 21/21 registries present, uniform (0 CRLF/indent/dup/4-digit/outside rows); S367/S372/S373/S390/S409 exist only in kake and kotodama with different sources each; kama and kasegi working trees differ from HEAD; main hazard is lane-local ids colliding across lanes.
