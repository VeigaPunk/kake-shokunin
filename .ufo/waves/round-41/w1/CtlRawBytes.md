# Round 41 w1 — CtlRawBytes (control: `loc` judged by regex over the raw file bytes)

No control reached 1434: the strongest non-decoding raw-bytes judge scores **1277/1434** (`loc` 473/630), the faithful control **1058** — both below the reference repair's 1434.
One tool did reach 1434 (`V3_decode_probe.py`) but it is **not** a control: it expands numeric character references and then applies the full RFC 3986 check, i.e. it does the named work with no XML parser. This counter therefore separates on "did you recover the `loc` character data", not on "did you call ElementTree" — the only reachable 1434 does the value judgment.

## Tools, receipts, and the work each skips (`--seed 41` unless noted; counter exit 0=met, 1=not met)
All tools in `/fast/scratch/hyaku/kake-r41w1/CtlRawBytes/`; every one keeps ref_fix's full RFC 3986 gate for `sitemapUrl` (804/804 in every run), so the whole deficit is `loc`.

- `V1_rawbytes.py` sha256 41372051009ebb245aafc88a091062107fc709f566ada200f56f849ac708ddf1 — passed **1058**, met false, exit 1, loc 254/630, sitemapUrl 804/804, byComponent fragment 163/239, host 170/239, path 165/239, port 227/239, query 169/239, userinfo 164/239 (random seed 41651018162074 → 1046, loc 242/630).
  Skips entity decoding and XML-value extraction: the judged string is the bytes between `<loc>` and `</loc>` (whitespace-stripped), then the full RFC 3986 gate + scope check. Caught by 373 of 397 oracle-valid loc cases — valid values are themselves escaped in the file (`c1_count.py:169-170`), e.g. value `Https://8leeDgK%41.net/aoo.wEcZr5` is written `Https:&#47;&#x2F;8leeDgK%41.net/...`, which is not a URI — plus 3 oracle-invalid locs whose offending character is hidden (`port` units `O`, `R`; `userinfo` unit `>`).
- `V10_literal_chars.py` sha256 e8ef6b1e1d479bdd65683bebbde35328cc62a40d1e7bf59cd75e724ae894ff2b — passed **1277**, met false, exit 1, loc 473/630, sitemapUrl 804/804, byComponent fragment 227/239, host 225/239, path 223/239, port 156/239, query 224/239, userinfo 222/239 (random seed 27093273905338 → 1280, loc 476/630).
  Skips all structure and every hidden character: only literal bytes are examined (characters RFC 3986 never allows, plus a literal `%` followed by fewer than two hex digits). Caught by the 157 oracle-invalid loc cases whose offending character sits behind a numeric reference; all 397 oracle-valid cases pass, so its deficit is exactly the invisible characters.
- `V2_rejectrefs.py` sha256 ce2614ad3d5d81524289177c97a5a385bcb57f9d2296be97d5e9f5b7aa3b205f — passed **1042**, met false, exit 1, loc 238/630, sitemapUrl 804/804, byComponent fragment 161/239, host 165/239, path 162/239, port 227/239, query 166/239, userinfo 161/239.
  V1 plus "any `&#` in the bytes ⇒ reject"; over-rejects: 159 extra oracle-valid locs lost versus V1.
- `V5_refs_accept.py` sha256 98b7f733c1c70a1ecbbb5a10605ba1e614fae9fd1958ccdbe1d5c620b74852d1 — passed **1202**, met false, exit 1, loc 398/630, sitemapUrl 804/804, byComponent fragment 214/239, host 210/239, path 211/239, port 147/239, query 208/239, userinfo 212/239.
  Gives up (accepts) whenever a reference is present; caught by 232 of 233 oracle-invalid locs.
- `V9_no_loc_judgment.py` sha256 47d6ce6d466d9a17ca36fb92ccec91737833d9e4b1e9e9f1f1f648cb6f3ddd27 — passed **1201**, met false, exit 1, loc 397/630, sitemapUrl 804/804, byComponent fragment 213/239, host 210/239, path 211/239, port 147/239, query 208/239, userinfo 212/239.
  Control floor: `loc` never judged; caught by all 233 oracle-invalid locs. Note V1 (1058) scores *below* this floor — honest raw-byte judging costs valid cases.
- `V3_decode_probe.py` sha256 d0e77e223d321cd61e6fe56a2df5a7dae45029a80f732a232fb9411bd488de23 — passed **1434**, met **true**, exit 0, loc 630/630, sitemapUrl 804/804, all components 239/239.
  **Boundary probe, not a control**: same raw regex, but it expands `&#N;`/`&#xN;`/named refs before the RFC 3986 gate. It does the named work (value judgment) without any XML parse.
- `V11_literal_plus_noref.py` (no counter receipt; offline harness only) — 1277, loc 473: V10 plus "no reference ⇒ also RFC-check the bytes"; identical score, so added nothing (0 invalid loc cases are both reference-free and V10-clean).
- baselines, my runs: `/fast/scratch/hyaku/kake-r41/shared/ref_fix.py` sha256 6d7c2dd445fc… → **1434**, met true, exit 0. `/fast/scratch/hyaku/kake-r41/shared/base.py` sha256 4de35f8c9d3e… → **1045**, exit 1, loc 508/630, sitemapUrl 537/804, byComponent fragment 163/239, host 162/239, path 157/239, port 238/239, query 158/239, userinfo 167/239.

## Commands (all run; receipts in `/fast/scratch/hyaku/kake-r41w1/CtlRawBytes/*.json`)
`prlimit --as=4000000000 timeout 900 python3 -B .ufo/waves/round-41/c1_count.py --root <lane> --tool-file <tool> --seed 41 --out <receipt>` → exit 1 for V1/V2/V5/V9/V10/base, exit 0 for V3/ref_fix; two random-seed runs (V1, V10) exit 1. Each ~3 s, ≤2 concurrent.
Offline cross-check (exact seed-41 corpus rebuilt with the counter's own `generate`/`layout` plus `main`'s three `getrandbits` draws; reproduced V1's 1058 exactly) gave per-case splits: V1 valid-ok 24 / valid-miss 373 / invalid-hit 230 / invalid-miss 3; V10 397/0/76/157; V5 397/0/1/232; V9 397/0/0/233.

## Findings
- `c1_count.py:166-170` (`xml_text`) escapes every C0/DEL and every `&<>"'` — and 30% of every other non-alnum character — to `&#N;`/`&#xN;`. So in `loc` files most *valid* values are not URIs in the bytes, and most *invalid* characters are invisible in the bytes. A raw-byte judge loses in both directions; escaping is applied per character (`LOC_UNITS`/`URL_UNITS`, `c1_count.py:45-46`).
- `c1_count.py:252-269` (`judge`): a `loc` case is answered only by a `loc_not_absolute` finding with the right entry (`:267`), so raw variants cannot be rescued by their other findings (`loc_out_of_scope` on valid locs is ignored, `:265` covers the `sitemapUrl` side).
- Measured ceiling of the class: with literal bytes only, the best split is 397 valid + 76 invalid = 473 loc cases (achieved by V10). The one extra literal signal available, imbalanced `[`/`]`, would catch 13 invalid and lose 14 valid (net −1), so 473 is where this class stops. The remaining 157 loc cases need the number inside a reference read, i.e. entity decoding if done by regex, or XML parsing if done with ElementTree.
- `ref_fix.py` scores 1434 through ElementTree; `V3` scores 1434 through a regex plus reference expansion — the counter credits the value judgment, not the parser (`c1_count.py:176-185` builds every case from one inserted character or percent sequence).
- `base.py` gets 508/630 on `loc` while V1 gets 254/630: refusing to decode is worse on `loc` than not checking at all, because escaped valid values then look illegal.

## Statement check
- "counter generates 1434 cases per run (630 `loc` + 804 `sitemapUrl`), one inserted ASCII character or percent sequence in one of six components" — **holds** (receipts `cases: 1434`, byField 630/804; `c1_count.py:45-46,176-185`).
- "predicate: agrees on 1434 of 1434" — **holds** (`main` sets `met` only at 1434 and exits 0 only then; `:252-269`).
- "base tool scores 1049" — **holds as stated for the L1's seed**; my seed-41 run gives 1045 (loc 508/630, url 537/804), so the figure is seed-dependent, not contradicted.
- "reference repair scores 1434" — **holds** (my seed-41 run: 1434, met true).
- "counter reads the lane only through read-only `git show`" — **holds for `--revision`**; with `--tool-file` it reads the named file and no lane file at all.
- "a control reaching 1434 makes the counter too weak" — no raw-bytes control reaches it; the single 1434 I produced performs the claimed value judgment, so it is not evidence against the counter.

## Files changed, risks, blockers
- Wrote only `/fast/scratch/hyaku/kake-r41w1/CtlRawBytes/` (7 tools, 7 receipts, debug corpus under `dbg/`) and this report. No tool installs. Lane, shared dir and round-41 wave dir untouched (read-only reads only).
- V1/V10 take entry structure and entry indices from ElementTree (which entry has a `loc`, scope-check inputs) and only the judged value from the raw regex, paired positionally with the `<loc>` matches — exact for this well-formed generated corpus, not a general parser. `MAX_LOC_CODEPOINTS` is applied to the raw text, so it is inflated by references (irrelevant at these sizes, a deliberate consequence of the skip).
- Scores are one fixed seed (41) plus one random seed each for V1 and V10 (1277 vs 1280; 1058 vs 1046). No blockers.
