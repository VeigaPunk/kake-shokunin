# MutC2Selftest

Round-56 W2 mutation probe: 40 single-point mutants of the eight `run_checks` condition blocks in
`c56_quote_truth.py` @ `a450e43e`, each run against its own selftest (`KAKE_R56_SELFTEST_REV=a450e43e...
python3 -B <mutant> --selftest`, exit != 0 = KILLED) in a private clone, the mutant written in place at the
counter's own path one at a time. Baseline: `67/67`, exit 0.

MUTANTS:

| id | attack point | mutation | result | killed by / note |
|----|--------------|----------|--------|------------------|
| M01 | :291 | `row[7] != "mined"` flipped to `==` | KILLED | `pass` case (flags every row) |
| M02 | :293 | drop opened-date check | SURVIVED | no fixture edits the row opened cell |
| M03 | :295 | drop row recheck-format check | SURVIVED | no fixture edits row[9] |
| M04 | :299 | drop kind/tier enum check | SURVIVED | :738 fixture edits REGISTRY only → C7 masks |
| M05 | :301 | drop 20-char scope/teaches floor | SURVIVED | no fixture shortens those cells |
| M06 | :304 | drop new-row-already-in-base | SURVIVED | base edits force mirror≠base (C8 :524) |
| M07 | :310 | drop prior-row-vs-base compare | SURVIVED | S367 cell edits trip C7 :498 / C8 :547 |
| M08 | :250 | drop staged-name-absent check | KILLED | `fail_staged_name_survives` |
| M09 | :248 | drop absent-entry check | SURVIVED | absent entry trips C2+C7 regardless |
| M10 | :271 | drop verified-at round-date check | SURVIVED | fixture edits entry only → C7 masks |
| M11 | :274 | drop header recheck-format check | SURVIVED | same C7 masking |
| M12 | :266 | drop source-line-names-sid check | SURVIVED | same C7 masking |
| M13 | :381 | drop `in_content` test in verify() | SURVIVED | boilerplate span excluded by :420 uniqueness |
| M14 | :346 | drop held-row body sha pin | KILLED | `fail_held_body_edited` |
| M15 | :89 | `MIN_UNIQUE_SPANS` 3→1 | SURVIVED | no fixture leaves 1-2 unique spans |
| M16 | :72 | `UNIT_CEILING` 25→50 | KILLED | assert in `fail_char_ceiling_44_chars_25_units` crashes case build — fragile coupling, not behavioral; behavioral killer proven (below) |
| M17 | :376 | drop CHAR_CEILING check | SURVIVED | 44-char fixture edits entry only → C7 masks |
| M18 | :401 | drop gate page-unique others/count | KILLED | `fail_gate_quote_shared_with_sibling` |
| M19 | :420 | entry unique test drops others/count | SURVIVED | shared-span fixtures use non-verbatim spans (`found=False`) |
| M20 | :403 | drop gate-line URL check | SURVIVED | no fixture strips a gate URL |
| M21 | :405 | drop gate-line access-date check | KILLED | `fail_lesson_no_date` |
| M22 | :392 | drop gate-line curly-quote check | SURVIVED | only entry-line curly (:412) has a fixture |
| M23 | :339 | drop 1000-byte body floor | SURVIVED | small bodies break title/URL/window/pins |
| M24 | :354 | drop row-anchor-in-body check | SURVIVED | REGISTRY-only edit → C7 masks |
| M25 | :456 | drop fetchedAt round-date/UTC check | KILLED | `fail_receipt_offset_nonutc`/`_stale`/`fail_receipt_stale_date` |
| M26 | :458 | drop userAgent round-tag check | KILLED | `fail_receipt_useragent_untagged` |
| M27 | :451 | drop httpStatus==200 check | KILLED | `fail_receipt_status` + `_bool` |
| M28 | :448 | drop receipt bytes check | SURVIVED | no bytes-only fixture |
| M29 | :498 | drop validated-vs-landed byte equality | KILLED | `fail_validated_doc_differs`, `fail_validated_row_differs` |
| M30 | :490 | drop E03/E04 stdout scan | SURVIVED | appended E04 line becomes stdout tail → tail-shape check masks |
| M31 | :488 | drop exit=0 check | KILLED | `fail_validate_exit` |
| M32 | :479 | drop --root-in-argv rejection | SURVIVED | `fail_validate_root_argv` argv lacks `--file` → first branch masks |
| M33 | :556 | drop strict-ancestor/earlier checks | SURVIVED | `_build` always adds the mirror 2 commits below tip |
| M34 | :547 | drop restored append-only compare | SURVIVED | REGISTRY-only edits trip C7; sid-cell edits trip rows-count |
| M35 | :524 | drop mirror-vs-base byte equality | KILLED | `fail_new_row_already_in_base` fires via C3 :304 (mutual masking pair with M06) |
| M36 | :563 | drop blob-at-add-commit sha pin | SURVIVED | blob ≡ mirror ≡ pin under `_build`; mirror-vs-pin sha masks |
| M37 | :567 | drop blob-carries-new-rows check | SURVIVED | blob ≡ mirror → redundant with new-row-in-mirror |
| M38 | :322 | drop used-by equality check | SURVIVED | REGISTRY-only edits → C7 masks |
| M39 | :60 | `ROUND_DATE` → "2026-10-24" | KILLED | `pass` case (all date checks flip) |
| M40 | :162 | `units()` drops non-CJK tokens | KILLED | unit rule "latin tokens counted per word" |

Tally: 14 KILLED, 26 SURVIVED. Attack points are `c56_quote_truth.py` line numbers at `a450e43e`; every mutant's old text was asserted to match exactly once before application.

SURVIVORS:

Systemic mask: any fixture that edits a landed entry or the registry WITHOUT making the identical edit in the
`assimilation/validate/` scratch copies keeps exit=1 via C7 byte-equality (:498), so it can never kill a
single-check drop in C2/C3/C4/C5 — this explains M04, M10, M11, M12, M17, M24, M38 (and weakens :738, :888,
:891, :831). 19 of the 26 survivors are killed by the validated fixtures below; the other 7 are structurally
masked, no `@case` can reach them: M06 :304 (any base edit containing S419 forces C8 :524), M07 :310 (C7 :498 +
C8 :547), M09 :248 (C2+C7 fire on any absent entry), M23 :339 (title/URL/window/pin checks co-fire), M33 :556
(`_build` commit graph fixed), M36 :563 + M37 :567 (blob ≡ mirror because `_build` never rewrites the mirror).

PROPOSED FIXTURES:

Validated against this rev: appended before `unit_checks = {`, each keeps the pristine selftest green
(exit 0, 68 cases) and makes its survivor's run FAIL on the new case only (`expected 1, got 0`). Shared
dual-edit helper (edits landed + validated copy so C7 stays satisfied):

```python
def dual(f, rel, a, b):
    f[rel] = f[rel].replace(a, b, 1)
    if rel == REGISTRY: f[VALIDATE_REG] = f[VALIDATE_REG].replace(a, b, 1)
    elif rel in ADOPTED.values(): f[f"{VALIDATE}/{rel}"] = f[f"{VALIDATE}/{rel}"].replace(a, b, 1)
```

```python
@case("fail_row_opened_not_round_date")
def _(f): dual(f, REGISTRY, row(f, "S419"), row(f, "S419").replace("| 2026-10-25 |", "| 2026-10-24 |", 1))  # kills M02
@case("fail_row_recheck_junk_dual")
def _(f): dual(f, REGISTRY, row(f, "S419"), row(f, "S419").replace("| 180d |", "| soon |", 1))              # kills M03
@case("fail_new_row_junk_kind_tier_dual")
def _(f): dual(f, REGISTRY, row(f, "S419"), row(f, "S419").replace("| docs | A |", "| spec | Z |", 1))       # kills M04
@case("fail_row_teaches_too_short")
def _(f):
    r = row(f, "S420"); parts = r.split("|"); parts[7] = " 短い "; dual(f, REGISTRY, r, "|".join(parts))      # kills M05
@case("fail_verified_at_wrong_date_dual")
def _(f): dual(f, ADOPTED["S420"], "verified-at: 2026-10-25", "verified-at: 1999-01-01")                     # kills M10
@case("fail_recheck_junk_cadence_dual")
def _(f): dual(f, ADOPTED["S420"], "recheck: 180d", "recheck: soon")                                         # kills M11
@case("fail_source_line_unnamed_dual")
def _(f):
    ln = next(l for l in f[ADOPTED["S367"]].splitlines()[:8] if re.match(r"^[-* ]*source *:", l)); dual(f, ADOPTED["S367"], ln, ln.replace("S367", "S368", 1))  # kills M12
@case("fail_gate_quote_outside_content")
def _(f):
    g = gate_line_of(f, "S367"); q = re.findall(r'"([^"]+)"', g)[-1]; f[LESSON] = f[LESSON].replace(g, g.replace(q, "特定のリンク先ウェブページの"))  # real S367 nav string, outside the content window; kills M13
@case("fail_entry_two_unique_spans")
def _(f):
    body = f[ADOPTED["S419"]]; text = f[f"{SOURCES_DIR}/S419.html"]
    others = [f[f"{SOURCES_DIR}/{s}.html"] for s in ("S367", "S420")]
    spans = [s for s in re.findall(r'"([^"]+)"', "\n".join(body.splitlines()[8:])) if units(s) >= 6 and text.count(s) == 1 and not any(s in t for t in others)][:2]
    new = "\n".join(ln for ln in body.split("\n") if '"' not in ln) + "".join(f'\n> "{s}"' for s in spans)
    f[ADOPTED["S419"]] = new; f[f"{VALIDATE}/{ADOPTED['S419']}"] = new                                        # kills M15
@case("fail_char_ceiling_dual")
def _(f): dual(f, ADOPTED["S419"], "recheck: 180d", 'recheck: 180d\n> "続けるときには、サーバーが「HTTP 404 Not Found」のステータスを返すよう"')  # kills M17
@case("fail_entry_nonunique_verbatim_spans")
def _(f):
    body = f[ADOPTED["S420"]]
    keep = [ln for ln in body.split("\n") if '"' not in ln]
    # spans verbatim in the retained body, but duplicated or shared with the S419 sibling body
    spans = ("存在しないウェブページが巡回される", "存在しないウェブページを表示しようとしたときに", "このような設定ができない場合には")
    new = "\n".join(keep) + "".join(f'\n> "{s}"' for s in spans); f[ADOPTED["S420"]] = new; f[f"{VALIDATE}/{ADOPTED['S420']}"] = new  # kills M19
@case("fail_gate_no_url")
def _(f):
    g = gate_line_of(f, "S367"); f[LESSON] = f[LESSON].replace(g, g.replace(ROW_URL["S367"], ""))             # kills M20
@case("fail_gate_curly_quote")
def _(f):
    g = gate_line_of(f, "S367"); f[LESSON] = f[LESSON].replace(g, g + " 補足 “この説明は補足ですよ”")          # kills M22
@case("fail_anchor_heading_not_in_body_dual")
def _(f): dual(f, REGISTRY, row(f, "S420"), row(f, "S420").replace("§ 存在しないウェブページが巡回される (更新日", "§ 存在しない見出し (更新日", 1))  # kills M24
@case("fail_receipt_bytes_off")
def _(f):
    r = jload(f, RECEIPTS); r["sources"]["S367"]["bytes"] += 1; f[RECEIPTS] = jdump(r)                        # kills M28
@case("fail_validate_e04_midstream")
def _(f):
    p = f"{VALIDATE}/census-stdout.txt"; lines = f[p].rstrip("\n").split("\n")
    lines.insert(len(lines) - 1, "file\tE04\tS420 duplicate source row"); f[p] = "\n".join(lines) + "\n"      # kills M30
@case("fail_validate_root_and_file_argv")
def _(f): f[f"{VALIDATE}/census-argv.txt"] = f"/x/sources-census.sh validate --file {VALIDATE_REG} --root /x\n"  # kills M32
@case("fail_not_append_only_cell_dual")
def _(f): dual(f, REGISTRY, row(f, "S263"), row(f, "S263").replace("| docs | A |", "| docs | B |", 1))        # kills M34
@case("fail_used_by_not_extended_dual")
def _(f): dual(f, REGISTRY, row(f, "S367"), set_used_by(row(f, "S367"), ADOPTED["S367"]))                     # kills M38
```

Behavioral backup for M16 (already assert-killed): appending the real in-content unique S419 span of 31 units
`メタタグを使ったインデックスへの登録拒否の設定を行ってください` to entry+validated copy flips pristine to exit 1 ("quotes 31
units, ceiling 25") and the ceiling-50 mutant to exit 0 (direct `run_checks` driver; the fixture-build assert
fires before any case inside the selftest itself).

For the 7 structural survivors the selftest needs runner-level power, not file fixtures: assert the expected
failing check id (`case(..., want=("C1_entries_exist", 1))`) for M06/M07/M09/M23, and `_build` variants —
mirror added at the tip commit (M33); mirror rewritten post-add-commit with an updated pin (M36/M37).

EVIDENCE:

- Clone `/tmp/mutc2.HrchmC` @ `a450e43e696d032e3ac308383f6b3394e0c92860` (toplevel = clone root); baseline
  `c56 quote-truth selftest: 67/67`, exit 0. Pristine counter sha256
  `e874e3005de88218a7710b7b654288e0006cef11d8793a3c2d095756e2b37196`, re-verified byte-identical after every
  mutant and validation run and at wave end (73 runs; each mutation asserted unique).
- No lane file, lane git index, or jj state touched; this report is the only lane write. Logs: `/tmp/mutc2.logs/`.

VERDICT: 40 mutants → 14 killed, 26 survive; 19 survivor kills delivered as validated `@case` fixtures (dual-edit pattern defeats the C7 mask), 7 structurally masked — the selftest needs check-id assertions and `_build` variants, not just more file fixtures.
